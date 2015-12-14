from filelock import FileLock

from quantdsl.application.base import BaseQuantDslApplication
from quantdsl.application.main import get_quantdsl_app
from quantdsl.infrastructure.celery.app import celery_app


class CeleryCallEvaluationQueueFacade(object):

    def put(self, item):
        dependency_graph_id, contract_valuation_id, call_id = item
        celery_evaluate_call.delay(dependency_graph_id, contract_valuation_id, call_id)


quantdsl_app = None


def get_quant_dsl_app_for_celery_worker():
    global quantdsl_app
    if quantdsl_app is None:
        quantdsl_app = get_quantdsl_app(call_evaluation_queue=CeleryCallEvaluationQueueFacade())
    return quantdsl_app


@celery_app.task
def celery_evaluate_call(dependency_graph_id, contract_valuation_id, call_id):

    quantdsl_app = get_quant_dsl_app_for_celery_worker()

    assert isinstance(quantdsl_app, BaseQuantDslApplication)

    quantdsl_app.evaluate_call_and_queue_next_calls(
        contract_valuation_id=contract_valuation_id,
        dependency_graph_id=dependency_graph_id,
        call_id=call_id,
        lock=FileLock('/tmp/quantdsl-results-lock'),
    )


@celery_app.task
def add(x, y):
    """
    An example task.
    """
    return x + y
