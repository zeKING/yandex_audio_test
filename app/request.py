import aiohttp


class AsyncRequest:

    @staticmethod
    async def form_result(response, response_type):
        body = None
        if response_type == 'json':
            body = await response.json()
        elif response_type == 'text':
            body = await response.text()
        elif response_type == 'file':
            body = await response.read()

        return {
            'status': response.status,
            'body': body,
            'headers': response.headers
        }

    @staticmethod
    async def get(url, response_type: str = 'json', **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, **kwargs) as response:
                return await AsyncRequest.form_result(response, response_type)

    @staticmethod
    async def post(url, response_type: str = 'json', **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, **kwargs) as response:
                return await AsyncRequest.form_result(response, response_type)


request = AsyncRequest()
