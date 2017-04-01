import arrow,os

TIMEZONE=os.environ['TIMEZONE']

def toLocal(time):
	return time.to(TIMEZONE)