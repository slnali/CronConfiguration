import unittest

from console_cron import getNearestTimeWhenCommandWillExecute


class MyTest(unittest.TestCase):

    def test_TaskWithMinutesAndHoursDailyExpectsTomorrow(self):
        time = "16:10"
        input = "30 1 command1"
        expectedOutput = "01:30 tomorrow - command1"
        self.assertEqual(getNearestTimeWhenCommandWillExecute(time,input), expectedOutput)


    def test_TaskWithMinutesAndHoursDailyExpectsToday(self):
        time = "16:10"
        input = "30 18 command1"
        expectedOutput = "18:30 today - command1"
        self.assertEqual(getNearestTimeWhenCommandWillExecute(time,input), expectedOutput)

    def test_TaskWithMinutesAndForAllHourValuesBeforeHour(self):
        time = "16:10"
        input = "45 * command1"
        expectedOutput = "16:45 today - command1"
        self.assertEqual(getNearestTimeWhenCommandWillExecute(time,input), expectedOutput)

    def test_TaskWithMinutesAndForAllHourValuesAfterHour(self):
        time = "16:10"
        input = "5 * command1"
        expectedOutput = "17:05 today - command1"
        self.assertEqual(getNearestTimeWhenCommandWillExecute(time,input), expectedOutput)

    def test_TaskWithMinutesAndForAllHourValuesAfterHourTomorrow(self):
        time = "23:10"
        input = "5 * command1"
        expectedOutput = "00:05 tomorrow - command1"
        self.assertEqual(getNearestTimeWhenCommandWillExecute(time,input), expectedOutput)

    def test_TaskWithAllMinutesAndForAllHourValues(self):
        time = "16:10"
        input = "* * command1"
        expectedOutput = "16:10 today - command1"
        self.assertEqual(getNearestTimeWhenCommandWillExecute(time,input), expectedOutput)


    def test_TaskWithAnyMinutesAndForHourValues(self):
        time = "16:10"
        input = "* 19 command1"
        expectedOutput = "19:00 today - command1"
        self.assertEqual(getNearestTimeWhenCommandWillExecute(time,input), expectedOutput)
