from django.contrib.auth import get_user_model

import pytest
from ..chat import views as chat_views
from ..chat.models import Message


User = get_user_model()


class TestChatViews:
    """ Create users, messages and set up relationships """
    @pytest.fixture
    def alex(self, db):
        return User(username='alex', password='test', id=1)

    @pytest.fixture
    def jake(self, db):
        return User(username='jake', password='test', id=2)

    @pytest.fixture
    def liz(self, db):
        return User(username='liz', password='test', id=3)

    @pytest.fixture
    def friends(self, alex, jake, liz):
        """ alex is friends with liz and jake """
        alex.friends.add(jake)
        alex.friends.add(liz)

        liz.friends.add(alex)
        jake.friends.add(alex)

        alex.save()
        liz.save()
        jake.save()

        return alex, jake, liz

    def test_build_messages_correct_users(self, friends):
        user_ids = sorted([x.id for x in friends])
        alex_id = user_ids[0]
        jake_id = user_ids[1]
        liz_id = user_ids[2]

        # alex sends "foo" to liz
        Message(author_id=alex_id, recipient_id=liz_id, body='foo').save()
        # alex sends "bar" to jake
        Message(author_id=alex_id, recipient_id=jake_id, body='bar').save()

        data = chat_views.messages(alex_id)

        # Prove that the keys correspond to the recipients of alex's message
        assert sorted(data.keys()) == [jake_id, liz_id]
        # Prove that alex said foo to liz, and bar to jake
        assert data[liz_id] == [('alex', 'foo')]
        assert data[jake_id] == [('alex', 'bar')]
