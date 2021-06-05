# from pytz import utc
# from utils.dataload import SQL
# # from classes.alliance import AllianceWar
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from discord.ext import commands
# from utils.dataload import SQL
# import os
# cwd = os.getcwd()


# class War(commands.Cog):
#     messages = 0

#     def __init__(self, client):
#         self.test_mode = True

#         self.client = client
#         self.alliances = []
#         self.times = SQL.select_war_times_all()
#         self.scheduler = AsyncIOScheduler()
#         # self.scan_register()
#         self.setup_schedule()
#         # self.scheduler.start()
#         # print(War.messages)

#     # def scan_register(self):
#     #     all_alliances = SQL.select_alliance_all()
#     #     for a in all_alliances:
#     #         A = AllianceWar(a.get('alliance_id'))
#     #         self.alliances.append(A)

#     def setup_schedule(self):
#         for alliance in self.alliances:
#             times = [time for time in self.times if time.zone == alliance.zone]
#             for time in times:
#                 self.schedule(time, alliance)
#             if self.test_mode == True and alliance.name == 'Agents of Z':
#                 self.schedule_test(alliance)

#     def schedule(self, time, alliance):
#         def func():
#             print(f'{alliance.name} at {time.hour}:{time.minute}')
#         self.scheduler.add_job(func, 'cron', day_of_week=time.day, hour=time.hour,
#                                minute=time.minute, second=time.second, timezone=utc, replace_existing=True)
#         War.messages += 1

#     def schedule_test(self, alliance):
#         from classes.time import Time
#         test = Time({"minute": "*", "hour": "*", "day": "*"})
#         self.schedule(test, alliance)
#         print(self.scheduler.get_jobs()[-1].trigger)


# def setup(client):
#     client.add_cog(War(client))
