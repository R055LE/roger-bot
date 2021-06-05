import discord
from discord.ext import commands
from pytz import utc
from apscheduler.schedulers.asyncio import AsyncIOScheduler
# sched = AsyncIOScheduler()
# sched.start()


class Cron(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.client.sched = AsyncIOScheduler()
        self.client.sched.start()

    async def schedule_cron(self, job_function, job_time, job_id=None):
        if job_id != None:
            self.client.sched.add_job(job_function, 'cron', day_of_week=job_time.get('day', '*'), hour=job_time.get(
                'hour', '*'), minute=job_time.get('minute', '*'), second=job_time.get('second', '0'), timezone=utc, replace_existing=True, id=job_id)
        else:
            self.client.sched.add_job(job_function, 'cron', day_of_week=job_time.get('day', '*'), hour=job_time.get(
                'hour', '*'), minute=job_time.get('minute', '*'), second=job_time.get('second', '0'), timezone=utc, replace_existing=True)

    async def pull_cron(self, job_id):
        job = self.client.sched.get_job(job_id)
        return job

    @commands.command(hidden=True)
    @commands.is_owner()
    async def cron(self, ctx):
        jobs = self.client.sched.get_jobs()
        print(len(jobs))


def setup(client):
    client.add_cog(Cron(client))
