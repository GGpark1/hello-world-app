"""
Test custom Django management commands.
"""
from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

"""
check : Command의 상태를 검사하는 메소드로,
database의 상태를 확인하기 위해 사용함(self.check(databases=['default']))

DB의 상태를 Mock하여 테스트를 외부(DB)에 의존하지 않고 진행하기 위해,
core.management.commands.wait_for_db.Command.check를 Mock함

check == false -> DB가 disable할 때 결과를 확인할 수 있음
check == true -> DB가 able할 때 결과를 확인할 수 있음
"""


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test command"""

    def test_wait_for_db_ready(self, patched_check):
        """
        Test waiting for database if database ready
        1. db.Command의 return_value를 True로 설정
        -> db가 available하다는 가정 아래 commanad가 의도대로 작동하는지 확인함
        2. call_command 실행 : 스크립트 안에서 execute로 명령어를 실행하면 오류가 발생함
        -> call_command로 return_value가 True인 wait_for_db 커맨드를 실행함
        3. return_value가 True인 상태의 wait_for_db command가 실행되었다면,
        check 메소드에 database의 정보를 저장함
        """
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    # sleep을 overriding하여 기존 코드의 sleep(1)을 초기화시킴
    # in-out으로 args order가 결정됨
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """
        Test waiting for database when getting OperationalError
        1. Psycopg 에러를 2번 일으키고,
        OperationError를 세번 일으키는 동안에도 wait_for 함수가 작동하는지 테스트
        2. 5번의 에러 끝에 True가 반환되었을 때,
        call_command('wait_for_db')가 기대한 값(=성공했을 때의 값)을 반환하는지 테스트
        """
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
