import logging
TEST_LOG = logging.getLogger("nexus-test")
TEST_LOG.setLevel(logging.INFO)
if not TEST_LOG.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('%(levelname)s | %(name)s | %(message)s')
    )
    TEST_LOG.addHandler(handler)