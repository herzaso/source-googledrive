REFRESH_URL = 'https://www.googleapis.com/oauth2/v4/token'

CONFIG = {
    'title': 'Google Drive',
    'icon': 'data:image/png;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBwgHBgkIBxQKCgkLDSIPDQwMGRYeFRAWICkeKSAdHyUkKDQoJCYxLh8nLT0lKTQtOjU6IzQ5RD0vQzQ1LisBCgoKDg0OGhAQGy8lICEyLTAwLzIrLS03NzY1LTUrNy41LS03LS8tODcyNy03LS8tLS0vNS83NzA3NS0wMi8tLf/AABEIADIAMgMBEQACEQEDEQH/xAAbAAACAgMBAAAAAAAAAAAAAAAABgUHAgMEAf/EADUQAAEDAgIFCQcFAAAAAAAAAAEAAgMEBRExEiFBYYEGBxMiQlHB0vEUFRYyUpLRI3GRsfD/xAAaAQACAwEBAAAAAAAAAAAAAAAABQMEBgEC/8QAKhEAAgECBQIGAgMAAAAAAAAAAAECAwQFERIxQRPRFSFRcZGhFLEyYYH/2gAMAwEAAhEDEQA/ALxQAIAi6e/UNS17qcukax5YXNwwxHFUK+I0qM9Ek/ruSUIdeGuDWRt97U/dJ/A/Kh8Yoej+F3JvxJ/0dkUjZY2vZra4YhMqVSNSCnHZleUXF5MzXs8ggAQAt8uL17stZghOFTUgtbhm1u0+HovMnkijf3HSp6VuxA5NXL2G49FKcIKjqux7Lth8PRK8Qt+rT1LeP6K+DXnRq6Jfxl++Ow8rNGxJOz1Oi4wPyOtv7p1hF1lLoy52Kd1TzWtEutCUAQBhNKyGJ8spDY2NLnOOQAzKDjaSzZTXKG7PvF1lqnYhmOjE09lgyHjxUDebMtc13WqOXwclvoZbnXQUcGuSV2juA2k7hmhbnKMHUmoLktCqojQ9HEC57QwAPdmcO/es1iNt0Kvls/NdjfW09UEnujQ1xY4ObqIOIKoRk4tSW6LDWayYyUk4qYGyDPJw7itlaXCr0lNf77iirT0SyNyskYj85F76GBlppz15Rpz4bG7Bxz9VHN8CjE7jJdJc7ldYqMSFlc3Nl9mo3XOoH6tQMIgeyzv4/wBDepYLkfYZb6Y9R7vb2GutpxU07mdoa2neoLy2Vek488e45o1NEsxcI0SQdRCxj8nkxuvM7LVVdBPoO+R+o7imOGXao1dLflIr3NLVHNbon1rBWIvOVZekhZdqcdePqT4bW7HcMuI7lHNcijFLfNdVcblck7BmVLa0HWqKPHIoo09csuDsp3EMDdepa6mslkX5G3SO9SHk8JXTgwcirR7yugllGNPTdd+OTnbB/u5UMRuelT0reRatKOueb2RaCzQ4MJ4o6iGSGYB8cjSx7TtBzCDkkpLJ8lay83NyFTIYJKQw6R6PTL9LR2Y4NzV+zuKVCOTTzfsK4YfKCaizNvN/dm9ui+5/lV9YpSXD+u56dlP1Rn8BXX66L7n+VevFqPo/ruc/BqeqD4Cuv10X3P8AKu+LUfR/Xc5+DU9UOvJ+1ss9sjpW4F/zSuHaec/xwSa6rutUc/j2GFGkqcFEklXJQQAIAEACABAAgAQB/9k=',  # noqa
    'params': [
        {
            'name': 'access_token',
            'title': 'Connect',
            'help': 'Authorize the Panoply.io Google Drive App',
            'type': 'oauth',
            'oauthAuthorizeURL': 'https://accounts.google.com/o/oauth2/v2/auth',  # noqa
            'oauthAccessURL': 'https://www.googleapis.com/oauth2/v4/token',
            'oauthRefreshURL': REFRESH_URL,
            'required': True
        },
        {
            'name': 'refresh_token',
            'type': '',
            'hidden': True
        },
        {
            'name': 'files',
            'title': 'Files',
            'required': True,
            'type': 'list',
            'values': [],
            'dependencies': ['access_token']
        }
    ],
    'categories': ['APIS', 'Files'],
    'keywords': ['googledrive', 'google', 'drive', 'gd', 'files'],
    'createdAt': '2017-05-29'
}
