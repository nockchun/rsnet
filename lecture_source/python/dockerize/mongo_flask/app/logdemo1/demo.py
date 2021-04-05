import logging

LOG = logging.getLogger(__name__)

def doLogging():
    LOG.debug("logdemo1: This is DEBUG log.")
    LOG.info("logdemo1: This is INFO log.")
    LOG.warning("logdemo1: This is WARNING log.")
    LOG.error("logdemo1: This is ERROR log.")
    LOG.critical("logdemo1: This is CRITICAL log.")
