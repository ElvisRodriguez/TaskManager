'''Class to format database rows into a flask-table object.
'''
from flask_table import ButtonCol, Col, Table


class ItemTable(Table):
    '''Converts a list of Item objects into a flask_table.Table object.

    Attributes:
        classes: HTML class names to be given to table when generated into HTML.
        task: flask_table.Col object that creates a column of all Item.task
              attributes and gives them an HTML class of 'task_row.'
        date: flask_table.Col object that creates a column of all Item.date
              attributes.
        clear: flask_table.ButtonCol object that creates a column of HTML
               buttons used to clear a table row by passing its ID to the
               'remove_task' app endpoint.
    '''
    classes = ['tasks_table']
    task = Col(name='Task', column_html_attrs={'class': 'task_row'})
    date = Col(name='Remind Me @')
    clear = ButtonCol(
        name='Clear Task',
        endpoint='remove_task',
        url_kwargs=dict(id='id'),
        button_attrs={'class': 'btn btn-default task-btn'}
    )


class Item(object):
    '''Creates an Item object to be used for ItemTable class.'''

    def __init__(self, id: int, task: str, date: str) -> None:
        '''Initializes Item object.

        Args:
            id: ID of user's task.
            task: Task of user of variable length (single and/or multiline)
            date: A timestamp in the format 'YYYY-MM-DD HH:MM'

        Returns:
            None.
        '''
        self.id = id
        self.task = task
        self.date = date


def objectify(rows: list) -> list:
    '''Converts a list of 3-tuples from todo_table database into Item objects.

    Args:
        rows: List of 3-tuples representing a task and its reminder date/time.

    Returns:
        A list, items, containing Item object representations of the tuples
        given.
    '''
    items = []
    for id, task, date in rows:
        item = Item(id, task, date)
        items.append(item)
    return items
