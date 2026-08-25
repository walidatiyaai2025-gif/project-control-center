#!/usr/bin/env python3
from __future__ import annotations
import json
import os
import random
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable

class GitHubAPIError(RuntimeError):
    def __init__(self, status:int, message:str, url:str):
        super().__init__(f"GitHub API {status}: {message} [{url}]")
        self.status=status; self.url=url

@dataclass(frozen=True)
class AuthContext:
    provider: str
    token: str | None
    write_capable: bool

def auth_from_env() -> AuthContext:
    # Provider order keeps credential material runtime-only.
    for env_name, provider, write_capable in (
        ("PCC_GITHUB_APP_TOKEN","github_app",True),
        ("PCC_GITHUB_WRITE_TOKEN","token_runtime",True),
        ("PCC_GITHUB_TOKEN","token_runtime",False),
        ("GITHUB_TOKEN","github_actions",False),
    ):
        token=os.getenv(env_name)
        if token:
            return AuthContext(provider,token,write_capable)
    return AuthContext("anonymous_public",None,False)

class GitHubClient:
    def __init__(
        self,
        auth:AuthContext|None=None,
        api_base:str="https://api.github.com",
        max_retries:int=5,
        timeout:int=30,
        sleep:Callable[[float],None]=time.sleep,
        opener:Callable[...,Any]|None=None,
    ):
        self.auth=auth or auth_from_env()
        self.api_base=api_base.rstrip("/")
        self.max_retries=max_retries
        self.timeout=timeout
        self.sleep=sleep
        self.opener=opener or urllib.request.urlopen

    def _headers(self)->dict[str,str]:
        h={"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28","User-Agent":"pcc-fleet-control"}
        if self.auth.token:
            h["Authorization"]=f"Bearer {self.auth.token}"
        return h

    def _url(self,path:str)->str:
        return path if path.startswith("http") else f"{self.api_base}{path}"

    def request_json(self, method:str, path:str, payload:dict|None=None)->Any:
        url=self._url(path)
        data=None if payload is None else json.dumps(payload).encode()
        last=None
        for attempt in range(self.max_retries+1):
            req=urllib.request.Request(url,data=data,headers=self._headers(),method=method)
            try:
                with self.opener(req,timeout=self.timeout) as r:
                    body=r.read()
                    return json.loads(body.decode() or "null")
            except urllib.error.HTTPError as e:
                last=e
                body=e.read().decode(errors="replace")
                remaining=e.headers.get("X-RateLimit-Remaining")
                retry_after=e.headers.get("Retry-After")
                reset=e.headers.get("X-RateLimit-Reset")
                retryable=e.code in {429,500,502,503,504} or (e.code==403 and remaining=="0")
                if not retryable or attempt>=self.max_retries:
                    raise GitHubAPIError(e.code, body[:500], url) from e
                delay=None
                if retry_after:
                    try: delay=float(retry_after)
                    except ValueError: pass
                if delay is None and reset:
                    try: delay=max(0.0,float(reset)-time.time()+1.0)
                    except ValueError: pass
                if delay is None:
                    delay=min(30.0,(2**attempt)+random.random())
                self.sleep(delay)
            except urllib.error.URLError as e:
                last=e
                if attempt>=self.max_retries:
                    raise RuntimeError(f"GitHub transport failed after retries: {url}: {e}") from e
                self.sleep(min(30.0,2**attempt))
        raise RuntimeError(f"GitHub request failed: {url}: {last}")

    def get(self,path:str)->Any: return self.request_json("GET",path)
    def put(self,path:str,payload:dict)->Any:
        if not self.auth.write_capable:
            raise PermissionError(f"auth provider {self.auth.provider} is not write-capable")
        return self.request_json("PUT",path,payload)

    def paginate(self,path:str, per_page:int=100, max_pages:int=50)->list:
        joiner="&" if "?" in path else "?"
        out=[]
        for page in range(1,max_pages+1):
            page_items=self.get(f"{path}{joiner}per_page={per_page}&page={page}")
            if not isinstance(page_items,list):
                raise RuntimeError(f"expected list from {path}")
            out.extend(page_items)
            if len(page_items)<per_page:
                break
        return out

    def repo(self,repo:str): return self.get(f"/repos/{repo}")
    def branches(self,repo:str): return self.paginate(f"/repos/{repo}/branches")
    def pulls(self,repo:str,state:str="open"): return self.paginate(f"/repos/{repo}/pulls?state={state}")
    def issues(self,repo:str,state:str="open"): return self.paginate(f"/repos/{repo}/issues?state={state}")
    def releases(self,repo:str): return self.paginate(f"/repos/{repo}/releases")
    def tags(self,repo:str): return self.paginate(f"/repos/{repo}/tags")
    def workflow_runs(self,repo:str,per_page:int=20):
        return self.get(f"/repos/{repo}/actions/runs?per_page={per_page}").get("workflow_runs",[])
    def branch_protection(self,repo:str,branch:str):
        try:
            return self.get(f"/repos/{repo}/branches/{urllib.parse.quote(branch,safe='')}/protection")
        except GitHubAPIError as e:
            if e.status in {404,403}: return None
            raise
    def content(self,repo:str,path:str):
        try:
            return self.get(f"/repos/{repo}/contents/{urllib.parse.quote(path,safe='/')}")
        except GitHubAPIError as e:
            if e.status==404: return None
            raise

    def protect_branch(self,repo:str,branch:str,required_contexts:list[str]):
        payload={
            "required_status_checks":{"strict":True,"contexts":required_contexts},
            "enforce_admins":True,
            "required_pull_request_reviews":{"dismiss_stale_reviews":True,"required_approving_review_count":1},
            "restrictions":None,
            "allow_force_pushes":False,
            "allow_deletions":False,
            "required_conversation_resolution":True,
        }
        return self.put(f"/repos/{repo}/branches/{urllib.parse.quote(branch,safe='')}/protection",payload)

    def upsert_text_file(self,repo:str,path:str,content:str,message:str,branch:str,sha:str|None=None):
        import base64
        payload={"message":message,"content":base64.b64encode(content.encode()).decode(),"branch":branch}
        if sha: payload["sha"]=sha
        return self.put(f"/repos/{repo}/contents/{urllib.parse.quote(path,safe='/')}",payload)
