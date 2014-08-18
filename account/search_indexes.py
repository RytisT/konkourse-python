from haystack import indexes
from models import UserProfile


class UserProfileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    user = indexes.CharField(model_attr='user')
    user_fullname = indexes.CharField(model_attr='user__get_full_name')
    content_auto = indexes.EdgeNgramField(model_attr='user__get_full_name')

    def get_model(self):
        return UserProfile

    def get_updated_field(self):
        return "modified"
