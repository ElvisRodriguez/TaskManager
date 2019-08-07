from flask_table import ButtonCol, Col, Table


class ItemTable(Table):
    task = Col('Task Name')
    date = Col('Task Event Date')
    clear = ButtonCol(
        'Clear Task', 'remove_task', url_kwargs=dict(id='id')
    )


class Item(object):
    def __init__(self, id, task, date):
        self.id = id
        self.task = task
        self.date = date


def objectify(rows):
    items = []
    for id, task, date in rows:
        item = Item(id, task, date)
        items.append(item)
    return items
