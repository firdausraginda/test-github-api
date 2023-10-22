import requests
import json
import os
import sys
from typing import List
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

# get credentials
creds_file = open(os.path.abspath("credentials.json"))
creds = json.load(creds_file)
creds_file.close()

# constant variables
GITHUB_API_TOKEN = creds["github_api_token_personal"]
URL_GITHUB_API = "https://api.github.com/repos/firdausraginda"
REPOSITORY_NAME = "test-github-api"


class GithubFunctionality:
    """Handle communication with github using github API"""

    def __init__(self) -> None:
        self.url_github_api = URL_GITHUB_API
        self.__headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {GITHUB_API_TOKEN}',
            'X-GitHub-Api-Version': '2022-11-28',
        }
    
    def write_pr_review(self, repo_name: str, pr_num: str, review_body: str) -> dict:
        """write a review on PR"""
        
        output = {
            "status": True,
            "data": {},
            "error": []
        }

        try:
            payload = json.dumps({
                "body": review_body,
                "event": "COMMENT"
            })

            response = requests.post(
                url=f"{URL_GITHUB_API}/{repo_name}/pulls/{pr_num}/reviews", 
                headers=self.__headers, 
                data=payload
            )

            if response.status_code != 200:
                raise Exception(f"[github_functionality - write_pr_review] write comment to PR '{pr_num}' is failed!")

        except Exception as e:
            output["status"] = False
            output["error"].append(f"[github_functionality - write_pr_review] {e}")

        else:
            output["data"] = response.status_code
        
        return output

    def request_review_on_pr(self, repo_name: str, pr_num: str, list_reviewer: List[str]) -> dict:
        """request reviewer on PR"""
        
        output = {
            "status": True,
            "data": {},
            "error": []
        }

        try:
            payload = json.dumps({
                "reviewers": list_reviewer,
                "team_reviewers": []
            })

            response = requests.post(
                url=f"{URL_GITHUB_API}/{repo_name}/pulls/{pr_num}/requested_reviewers",
                headers=self.__headers,
                data=payload
            )

            if response.status_code != 201:
                raise Exception(f"[github_functionality - request_review_on_pr] request reviewer on PR '{pr_num}' is failed!")

        except Exception as e:
            output["status"] = False
            output["error"].append(f"[github_functionality - request_review_on_pr] {e}")

        else:
            output["data"] = response.status_code

        return output
    
    def remove_reviewer_from_pr(self, repo_name: str, pr_num: str, list_reviewer: List[str]) -> dict:
        "remove reviewer from PR"

        output = {
            "status": True,
            "data": {},
            "error": []
        }

        try:
            payload = json.dumps({
                "reviewers": list_reviewer,
                "team_reviewers": []
            })

            response = requests.delete(
                url=f"{URL_GITHUB_API}/{repo_name}/pulls/{pr_num}/requested_reviewers",
                headers=self.__headers,
                data=payload
            )

            if response.status_code != 200:
                raise Exception(f"[github_functionality - remove_reviewer_from_pr] remove reviewer from PR '{pr_num}' is failed!")

        except Exception as e:
            output["status"] = False
            output["error"].append(f"[github_functionality - remove_reviewer_from_pr] {e}")

        else:
            output["data"] = response.status_code

        return output

    def get_branch_reference(self, repo_name: str, ref: str) -> dict:
        "get reference in a branch"

        output = {
            "status": True,
            "data": {},
            "error": []
        }

        try:
            response = requests.get(
                url=f"{URL_GITHUB_API}/{repo_name}/git/ref/{ref}",
                headers=self.__headers
            )

        except Exception as e:
            output["status"] = False
            output["error"].append(f"[github_functionality - get_branch_reference] {e}")

        else:
            output["data"] = response.json()

        return output
    
    def create_branch(self, repo_name: str, new_ref_name: str, sha: str) -> dict:
        "create branch"

        output = {
            "status": True,
            "data": {},
            "error": []
        }

        try:         
            payload = json.dumps({
                "ref": f"refs/heads/{new_ref_name}", 
                "sha": f"{sha}"
            })

            response = requests.post(
                url=f"{URL_GITHUB_API}/{repo_name}/git/refs",
                headers=self.__headers,
                data=payload
            )

        except Exception as e:
            output["status"] = False
            output["error"].append(f"[github_functionality - create_branch] {e}")

        else:
            output["data"] = response.json()

        return output
    
    def create_blobs(self, repo_name: str) -> dict:
        "create git blobs"

        output = {
            "status": True,
            "data": {},
            "error": []
        }

        try:
            payload = json.dumps({
                "content": "Content of the blob",
                "encoding": "utf-8"
            })

            response = requests.post(
                url=f"{URL_GITHUB_API}/{repo_name}/git/blobs",
                headers=self.__headers,
                data=payload
            )

        except Exception as e:
            output["status"] = False
            output["error"].append(f"[github_functionality - create_blobs] {e}")

        else:
            output["data"] = response.json()

        return output
    
    def get_tree(self, repo_name: str, branch: str) -> dict:
        "get tree"

        output = {
            "status": True,
            "data": {},
            "error": []
        }

        try:
            response = requests.get(
                url=f"{URL_GITHUB_API}/{repo_name}/git/trees/{branch}",
                headers=self.__headers
            )

        except Exception as e:
            output["status"] = False
            output["error"].append(f"[github_functionality - get_tree] {e}")

        else:
            output["data"] = response.json()

        return output
    
    def post_tree(self, repo_name: str) -> dict:
        "post tree"

        output = {
            "status": True,
            "data": {},
            "error": []
        }

        try:
            # data = '{"base_tree":"9fb037999f264ba9a7fc6274d15fa3ae2ab98312","tree":[{"path":"file.rb","mode":"100644","type":"blob","sha":"44b4fc6d56897b048c772eb4087f854f46256132"}]}'
            payload = json.dumps({
                "tree": [
                    {
                        "path":"helloworld/main.py",
                        "mode":"100644",
                        "type":"blob",
                        "sha":"929246f65aab4d636cb229c790f966afc332c124"
                    }
                ],
                "base_tree": "9530a16ee4445775be609b8ed855f6abb719d08c"
            })

            response = requests.post(
                url=f"{URL_GITHUB_API}/{repo_name}/git/trees",
                headers=self.__headers,
                data=payload
            )

        except Exception as e:
            output["status"] = False
            output["error"].append(f"[github_functionality - post_tree] {e}")

        else:
            output["data"] = response.json()

        return output
    
    
if __name__ == "__main__":
    # pr_num = "1"
    github_func_obj = GithubFunctionality()

    # ------------------------------------------------------------------

    # review_body = "testing comment 1"
    # res = github_func_obj.write_pr_review(REPOSITORY_NAME, pr_num, review_body)

    # ------------------------------------------------------------------

    # from src.lib.model import GithubUserNameDetail
    # github_user_name_detail_obj = GithubUserNameDetail()
    # list_reviewer = [item.name for item in github_user_name_detail_obj.detail]
    # res = github_func_obj.request_review_on_pr(REPOSITORY_NAME, pr_num, list_reviewer)
    # print(res)

    # ------------------------------------------------------------------

    # from src.lib.model import GithubUserNameDetail
    # github_user_name_detail_obj = GithubUserNameDetail()
    # list_reviewer = [item.name for item in github_user_name_detail_obj.detail]
    # res = github_func_obj.remove_reviewer_from_pr(REPOSITORY_NAME, pr_num, list_reviewer)
    # print(res)

    # ------------------------------------------------------------------

    # ref = "heads/branch-1"
    # ref = "heads/branch-2"
    # res = github_func_obj.get_branch_reference(REPOSITORY_NAME, ref)
    # print(json.dumps(res))

    # ------------------------------------------------------------------

    # new_ref_name = "branch-2"
    # sha = "9530a16ee4445775be609b8ed855f6abb719d08c"
    # res = github_func_obj.create_branch(REPOSITORY_NAME, new_ref_name, sha)
    # print(json.dumps(res))

    # ------------------------------------------------------------------

    # res = github_func_obj.create_blobs(REPOSITORY_NAME)
    # print(json.dumps(res))

    # ------------------------------------------------------------------

    # new_branch = "branch-2"
    # res = github_func_obj.get_tree(REPOSITORY_NAME, new_branch)
    # print(json.dumps(res))

    # ------------------------------------------------------------------

    # res = github_func_obj.post_tree(REPOSITORY_NAME)
    # print(json.dumps(res))