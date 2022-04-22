import requests
from typing import List
from uuid import uuid4

from models.doc import *
from models.group import *
from models.info import *
from models.repo import *
from models.user import *


class YuqueBaseClient(object):
    """Reference: https://www.yuque.com/yuque/developer/"""

    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://www.yuque.com/api/v2"
        self.user: UserDetailInfo = self.user_get_info()

    def _http_request(self, method: str, sub_url: str, params=None):
        url = self.base_url + sub_url
        response = requests.request(method=method, url=url, params=params,
                                    headers={'X-Auth-Token': self.token})
        if method == 'GET':
            return response.json() if response.status_code == 200 else {}
        else:
            return response.status_code == 200, response.json()

    def _http_get(self, sub_url: str, params=None):
        return self._http_request('GET', sub_url, params)

    def _http_post(self, sub_url: str, params=None):
        return self._http_request('POST', sub_url, params)

    def _http_put(self, sub_url: str, params=None):
        return self._http_request('PUT', sub_url, params)

    def _http_delete(self, sub_url: str, params=None):
        return self._http_request('DELETE', sub_url, params)

    ############################################################################
    #  user 用户 相关接口: https://www.yuque.com/yuque/developer/user
    ############################################################################
    def list_users_of_group(self, g_login_or_id) -> List[GroupUserData]:
        data = self._http_get(sub_url=f'/groups/{g_login_or_id}/users')
        return [GroupUserData(**user) for user in data['data']] if data else None

    def user_get_info(self, u_login_or_id=None) -> UserDetailInfo:
        if u_login_or_id:
            data = self._http_get(sub_url=f'/users/{u_login_or_id}').get('data')
        else:
            data = self._http_get(sub_url='/user').get('data')
        return UserDetailInfo(**data) if data else None

    ############################################################################
    #  group 组织 相关接口: https://www.yuque.com/yuque/developer/group
    ############################################################################
    def list_groups_of_user(self, u_login_or_id=None) -> List[GroupData]:
        u_login_or_id = self.user.id if not u_login_or_id else u_login_or_id
        groups = self._http_get(sub_url=f'/users/{u_login_or_id}/groups').get('data')
        return [GroupData(**group) for group in groups] if groups else []

    def list_groups_in_public(self) -> List[GroupData]:
        groups = self._http_get(sub_url=f'/groups').get('data')
        return [GroupData(**group) for group in groups] if groups else []

    def create_group(self, name: str, login: str, description: str = ''):
        params = {'name': name, 'login': login, 'description': description}
        result, data = self._http_post(sub_url=f'/groups', params=params)
        obj_data = GroupData(**data['data']) if result else ErrorInfo(**data)
        return result, obj_data

    def group_get_info(self, g_login_or_id) -> GroupDetailInfo:
        result = self._http_get(sub_url=f'/groups/{g_login_or_id}')
        return GroupDetailInfo(**result) if result else None

    def group_update_info(self, g_login_or_id, new_name: str = None,
                          new_login: str = None, new_description: str = None):
        params = {}
        if new_name:
            params.update({'name': new_name})
        if new_login:
            params.update({'login': new_login})
        if new_description:
            params.update({'description': new_description})
        params = None if not params else params
        result, data = self._http_put(sub_url=f'/groups/{g_login_or_id}', params=params)
        obj_data = GroupData(**data['data']) if result else ErrorInfo(**data)
        return result, obj_data

    def delete_group(self, g_login_or_id):
        """删除 Group"""
        result, data = self._http_delete(sub_url=f'/groups/{g_login_or_id}')
        obj_data = GroupData(**data['data']) if result else ErrorInfo(**data)
        return result, obj_data

    def group_add_user(self, g_login_or_id, u_login_or_id, admin: bool = False):
        return self.group_update_user(g_login_or_id, u_login_or_id, admin)

    def group_update_user(self, g_login_or_id, u_login_or_id, admin: bool = False):
        params = {'role': 1} if admin else {'role': 0}
        result, data = self._http_put(sub_url=f'/groups/{g_login_or_id}/users/{u_login_or_id}',
                                      params=params)
        obj_data = GroupUserData(**data['data']) if result else ErrorInfo(**data)
        return result, obj_data

    def group_delete_user(self, g_login_or_id, u_login_or_id):
        result, data = self._http_delete(sub_url=f'/groups/{g_login_or_id}/users/{u_login_or_id}')
        obj_data = self.user_get_info(
            u_login_or_id=data['data']['user_id']) if result else ErrorInfo(**data)
        return result, obj_data

    ############################################################################
    #  repo 知识库 相关接口: https://www.yuque.com/yuque/developer/repo
    ############################################################################
    def list_repos_of_user(self, u_login_or_id=None):
        u_login_or_id = self.user.id if not u_login_or_id else u_login_or_id
        data = self._http_get(sub_url=f'/users/{u_login_or_id}/repos').get('data')
        return [RepoBaseInfo(**repo) for repo in data] if data else []

    def list_repos_of_group(self, g_login_or_id):
        data = self._http_get(sub_url=f'/groups/{g_login_or_id}/repos').get('data')
        return [RepoBaseInfo(**repo) for repo in data] if data else []

    def create_repo_for_group(self, g_login_or_id, name: str, slug: str = uuid4().hex[:8],
                              description: str = '', public: int = 0,
                              type_: str = 'Book') -> RepoData:
        """
        public: 0 小组成员可见, 1 互联网可见, 4 知识库成员可见
        type_: 'Book' 普通文档文库, 'Thread' 话题知识库, 'Design' 图片知识库, 'Resource' 资源知识库, 默认 Book
        """
        params = {'name': name, 'slug': slug, 'description': description,
                  'public': public, 'type': type_}
        result, data = self._http_post(sub_url=f'/groups/{g_login_or_id}/repos', params=params)
        obj_data = RepoData(**data['data']) if result else ErrorInfo(**data)
        return result, obj_data

    def create_repo_for_user(self, name: str,
                             u_login_or_id=None, slug: str = uuid4().hex[:8],
                             description: str = '', public: int = 0,
                             type_: str = 'Book') -> RepoData:
        """
        public: 0 仅自己可见, 1 互联网可见
        type_: 'Book' 普通文档文库, 'Thread' 话题知识库, 'Design' 图片知识库, 'Resource' 资源知识库, 默认 Book
        """
        u_login_or_id = self.user.id if not u_login_or_id else u_login_or_id
        params = {'name': name, 'slug': slug, 'description': description,
                  'public': public, 'type': type_}
        result, data = self._http_post(sub_url=f'/users/{u_login_or_id}/repos', params=params)
        obj_data = RepoData(**data['data']) if result else ErrorInfo(**data)
        return result, obj_data

    def repo_get_info(self, r_namespace_or_id) -> RepoDetailInfo:
        result = self._http_get(sub_url=f'/repos/{r_namespace_or_id}')
        return RepoDetailInfo(**result) if result else None

    def repo_update_info(self, r_namespace_or_id,
                         new_name: str = None, new_slug: str = None, new_toc: str = None,
                         new_description: str = None, new_public: int = None):
        params = {}
        if new_name:
            params.update({'name': new_name})
        if new_slug:
            params.update({'slug': new_slug})
        if new_toc:
            params.update({'toc': new_toc})
        if new_description:
            params.update({'description': new_description})
        if new_public:
            params.update({'public': new_public})
        params = None if not params else params
        result, data = self._http_put(sub_url=f'/repos/{r_namespace_or_id}', params=params)
        obj_data = RepoData(**data['data']) if result else ErrorInfo(**data)
        return result, obj_data

    def delete_repo(self, r_namespace_or_id):
        result, data = self._http_delete(sub_url=f'/repos/{r_namespace_or_id}')
        obj_data = RepoData(**data['data']) if result else ErrorInfo(**data)
        return result, obj_data

    ############################################################################
    #  doc 文档 相关接口: https://www.yuque.com/yuque/developer/doc
    ############################################################################
    def list_docs_of_repo(self, r_namespace_or_id):
        """需要 Repo 的 abilities.read 权限"""
        data = self._http_get(sub_url=f'/repos/{r_namespace_or_id}/docs').get('data')
        return [DocBaseInfo(**doc) for doc in data] if data else []

    def create_doc(self, r_namespace_or_id,
                   title: str, body: str, format_: str = 'markdown',
                   public: int = 0, slug: str = uuid4().hex[:8]) -> DocData:
        format_ = 'markdown' if format_ not in DOC_FORMATS else format_
        params = {'title': title, 'slug': slug, 'body': body,
                  'public': public, 'format': format_}
        result, data = self._http_post(sub_url=f'/repos/{r_namespace_or_id}/docs',
                                       params=params)
        obj_data = DocData(**data['data']) if result else ErrorInfo(**data)
        return result, obj_data

    def doc_get_info(self, r_namespace: str, d_slug: str) -> DocDetailInfo:
        data = self._http_get(sub_url=f'/repos/{r_namespace}/docs/{d_slug}')
        return DocDetailInfo(**data) if data else None

    def doc_update_info(self, r_namespace_or_id, doc_id: int,
                        new_title: str = None, new_body: str = None, new_public: int = 0,
                        new_slug: str = None, _force_asl: int = 0) -> DocData:
        params = {'title': new_title, 'slug': new_slug, 'body': new_body,
                  'public': new_public, '_force_asl': _force_asl}
        result, data = self._http_put(sub_url=f'/repos/{r_namespace_or_id}/docs/{doc_id}',
                                      params=params)
        obj_data = DocData(**data['data']) if result else ErrorInfo(**data)
        return result, obj_data

    def delete_doc(self, r_namespace_or_id, doc_id: int):
        result, data = self._http_delete(sub_url=f'/repos/{r_namespace_or_id}/docs/{doc_id}')
        obj_data = DocData(**data['data']) if result else ErrorInfo(**data)
        return result, obj_data
