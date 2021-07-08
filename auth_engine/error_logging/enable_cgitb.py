
import cgitb


def enable_cgitb():
	
	cgitb.enable(display=1, logdir="./errors")


enable_cgitb()
