from app import db, redis_client
from nft.database.models.activity import Activity
from nft.database.models.users import Users
from nft.helpers.user_accounts import get_user_id_type
from constants import message_templates
from datetime import datetime

import sqlalchemy
import uuid


class Activity_MGR:

    @staticmethod
    def add_activity(**kwargs):
        db.session.add(Activity(user_id=kwargs['user_id'],
                                activity_id=uuid.uuid4().hex,
                                ip="",
                                user_agent="",
                                activity=kwargs['activity'],
                                url=""))
        db.session.commit()


    def get_user_activity(self, user_id, filter_by_activity_type=None):
        user_id_type = get_user_id_type(user_id)

        user = eval("""Users.query.filter_by({0}="{1}").first()""".format(user_id_type, user_id))

        if filter_by_activity_type is None:
            query = sqlalchemy.text("""
            
                SELECT * FROM `black-pearl-nft`.`activity` 
                WHERE (`user_id` = '{0}') 
                OR (`user_id` = '{1}' ORDER BY `time` DESC);
                
                """.format(user.username, user.email))

        else:
            query = sqlalchemy.text("""
            
            SELECT *
            FROM `black-pearl-nft`.`activity`
            WHERE (`user_id` = '{0}' OR `user_id` = '{1}')
            AND (`activity` = '{2}') ORDER BY time DESC;
            
            """.format(user.username, user.email, filter_by_activity_type))

        result = db.session.execute(query).fetchall()

        activity_history = {}
        for count, result in enumerate((dict(row) for row in result)):
            activity_history[count] = {
                "activity_id": result['activity_id'],
                "user_id": result['user_id'],
                "ip": result['ip'],
                "user_agent": result['user_agent'],
                "time": result['time'].strftime("%m/%d/%Y, %H:%M:%S"),
                "activity": result['activity'],
                "url": result['url']
            }

        return activity_history

    def add_failed_login_attempt(self, user_id, request):
        self.add_activity(user_id=user_id,
                          ip=str(request.remote_addr),
                          user_agent=str(request.user_agent),
                          activity='failed_login_attempt',
                          url=str(request.url))
        return

    def manage_login_attempts(self, user_id, request):

        self.add_failed_login_attempt(user_id, request)

        failed_login_attempts = self.get_user_activity(user_id=user_id, filter_by_activity_type="failed_login_attempt")

        """Check time elapsed since the fifth login attempt"""
        if 4 in failed_login_attempts:
            fifth_attempt_time       = datetime.strptime(failed_login_attempts[4]['time'], "%m/%d/%Y, %H:%M:%S")
            time_elapsed_since_fifth = (datetime.utcnow() - fifth_attempt_time).total_seconds() / 60

            """If less than 120 minutes have elapsed since last fifth attempt block the user account"""
            if int(time_elapsed_since_fifth) < 120:
                redis_client.set('{0}_account_blocked'.format(user_id), 1)
                return {"success": False,
                        "message": message_templates[1]}


        """Check time elapsed since the third login attempt"""
        if 2 in failed_login_attempts:
            third_attempt_time       = datetime.strptime(failed_login_attempts[2]['time'], "%m/%d/%Y, %H:%M:%S")
            time_elapsed_since_third = (datetime.utcnow() - third_attempt_time).total_seconds() / 60

            if int(time_elapsed_since_third) < 5:
                return {"success": False,
                        "message": message_templates[2]}

        return {"success": False,
                "message": "Invalid account password"}


activity_mgr = Activity_MGR()
