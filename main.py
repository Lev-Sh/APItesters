from pybit.unified_trading import HTTP

import requests
import json
import datetime
import pygame
BACKGROUND = pygame.Color(0, 100, 100)
pygame.init()
clock = pygame.time.Clock()

# Set up the API key (optional)
FPS = 900


def get_ticker():
    response = requests.get("https://api.bybit.com/v2/public/tickers?symbol=BTCUSD")
    data = json.loads(response.text)
    return data["result"][0]['last_price']


if __name__ == "__main__":
    width, height = 500, 500
    screen = pygame.display.set_mode((width, height))
    running = True
    font = pygame.font.SysFont("New Roman", 30)
    corner_x = 10
    corner_y = 10
    pygame.display.flip()
    GREEN_COLOR = (100, 255, 25)
    RED_COLOR = (255, 25, 25)
    btc_now = float(get_ticker())
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        BTC_price = float(get_ticker())
        if btc_now >= BTC_price:

            text = font.render(str(BTC_price), True, RED_COLOR)
            btc_now = BTC_price
        else:
            text = font.render(str(BTC_price), True, GREEN_COLOR)
            btc_now = BTC_price
        text_width, text_height = text.get_size()
        screen.fill(BACKGROUND)
        screen.blit(text, (corner_x, corner_y))

        pygame.display.update()
        clock.tick(FPS)
