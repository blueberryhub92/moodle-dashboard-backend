from pyodide.http import pyfetch
import asyncio


async def load_data():
    response = await pyfetch(url='/api/group/assessment', method='GET')
    output = await response.json()

    content_div = Element('content')
    content_div.element.innerHTML = output
