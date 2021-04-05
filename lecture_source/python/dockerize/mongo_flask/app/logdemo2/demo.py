import logging

LOG = logging.getLogger(__name__)

def doLogging():
    LOG.debug("logdemo2: This is DEBUG log.")
    LOG.info("logdemo2: This is INFO log.")
    LOG.warning("logdemo2: This is WARNING log.")
    LOG.error("logdemo2: This is ERROR log.")
    LOG.critical("logdemo2: This is CRITICAL log.")
