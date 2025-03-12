import json

import requests

sonar_url = "http://10.17.2.69:9000/api/"
sonar_auth = ("7e2cd1c883efe53ea0842ee60d8804d24c3372da", "")


def notify_sonar_bug():
    author_issues_list = sorted(request_project_issues(), key=lambda e: e.__getitem__('bug_count'))
    webhook_data_list = []
    for author_issues in author_issues_list:
        author = author_issues["author"]
        bug_count = author_issues["bug_count"]
        project_issues_map = author_issues["project_issues_map"]
        webhook_title = "用户【" + author + "】未解决BUG数量" + str(bug_count) + "个\n"
        webhook_content = ""
        for project, project_issues in project_issues_map.items():
            webhook_content += "项目 [" + project + "] 数量\n"
            for severity, count in project_issues.items():
                webhook_content += "<font color=\"green\">" + severity + "</font> = <font color=\"red\">" + str(count) + "</font>\n"
        mentioned_list = []
        if bug_count > 0:
            mentioned_list.append(author)
            webhook_content += "sonar地址：[点击跳转](http://10.17.2.69:9000/projects)"
        webhook_data_list.append({"content": webhook_content, "mentioned_list": mentioned_list, "bug_count": bug_count, "webhook_title": webhook_title})
    for webhook_data in webhook_data_list:
        webhook_content = webhook_data["content"]
        webhook_title = webhook_data["webhook_title"]
        webhook_params = markdown_webhook_message(webhook_title, webhook_content)
        headers = {'content-type': 'application/json'}
        response = requests.post(
            url="https://open.feishu.cn/open-apis/bot/v2/hook/ab105da7-2cd3-444c-94ec-f6b8ecf55139",
            headers=headers,
            data=json.dumps(webhook_params).encode('utf-8'))
        print(response.status_code, end="\n")


def request_project_issues():
    author_params = {"p": 1, "ps": 100}
    response = requests.get(url=sonar_url + "users/search", params=author_params, auth=sonar_auth)
    if response.status_code != 200:
        return []
    users = json.loads(response.text)["users"]
    author_issues_list = []
    for user in users:
        author = user["name"]
        groups = user["groups"]
        if "pjg" not in groups:
            continue
        author_issues_list.append(request_author_user(author))
    author_issues_list.append(request_author_user(''))
    return author_issues_list


def request_author_user(author: str):
    search_params = {"p": 1, "ps": 100, "statuses": "OPEN,CONFIRMED,REOPENED", "resolved": "false", "types": "BUG"}
    if len(author) > 0:
        search_params["assigned"] = "true"
        search_params["assignees"] = author
    else:
        search_params["assigned"] = "false"
    response = requests.get(url=sonar_url + "issues/search", params=search_params, auth=sonar_auth)
    if response.status_code != 200:
        return []
    json_issues = json.loads(response.text)["issues"]
    project_issues_map = {}
    bug_count = 0
    for json_issue in json_issues:
        project = json_issue["project"]
        if project not in project_issues_map:
            project_issues_map[project] = {}
        project_issues = project_issues_map[project]
        severity = json_issue["severity"]
        if severity not in project_issues:
            project_issues[severity] = 0
        bug_count += 1
        project_issues[severity] += 1
    return {"author": author, "bug_count": bug_count, "project_issues_map": project_issues_map}


def markdown_webhook_message(title: str, content: str) -> str:
    markdown = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": "green",
                "title": {
                    "content": title,
                    "tag": "plain_text"
                }
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": content
                }
            ]
        }
    }
    return markdown


if __name__ == '__main__':
    notify_sonar_bug()
