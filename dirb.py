#!/usr/bin/env python3

import argparse
import sys
import io
from tornado.httpclient import AsyncHTTPClient, HTTPClientError
import asyncio
from typing import Iterable, Callable

class Dirbuster:
    def __init__(self, 
                 root_url: str,
                 paths: Iterable[str],
                 pre_fetch_callback: Callable[[str], None] | None = None,
                 found_callback: Callable[[str], None] | None = None,
                 n_workers: int = 10) -> None:
        self.root_url = root_url
        self.found_callback = found_callback
        self.pre_fetch_callback = pre_fetch_callback
        self.paths = set([path.strip() for path in paths])
        self.queue = asyncio.Queue()
        self.n_workers = n_workers
        self._dead = []
        self._alive = []

    async def run(self) -> None:
        for url in self.paths:
            await self.queue.put(url)
        workers = [asyncio.create_task(self.worker()) for _ in range(self.n_workers)]
        await self.queue.join()
        for worker in workers:
            worker.cancel()

    async def grab(self) -> None:
        path = await self.queue.get()
        url = f'{self.root_url}{path}'
        if self.pre_fetch_callback is not None:
            self.pre_fetch_callback(url)
        try:
            http_client = AsyncHTTPClient()
            response = await http_client.fetch(url)
            if response.code == 200:
                self._alive.append(url)
                if self.found_callback is not None:
                    self.found_callback(url)
        except HTTPClientError as e:
            if e.code != 404:
                print(f'HTTP error for {path}: {e.code}', file=sys.stderr)
            self._dead.append(url)
        finally:
            self.queue.task_done()

    async def worker(self) -> None:
        while True:
            try:
                await self.grab()
            except asyncio.CancelledError:
                return

    @property
    def alive(self) -> Iterable[str]:
        return self._alive

    @property
    def dead(self) -> Iterable[str]:
        return self._dead


def pre_fetch_hook(url: str) -> None:
    print(f'\rTrying {url} ...')


def found_hook(url: str) -> None:
    print(f'\rFOUND {url}.')


async def main(server: str, verbose: int, paths: io.StringIO):
    found_callback = found_hook if verbose > 0 else None
    pre_fetch_callback = pre_fetch_hook if verbose > 0 else None
    dirb = Dirbuster(server, paths.readlines(), pre_fetch_callback, found_callback, 8)
    await dirb.run()
    print('Found:')
    for result in dirb.alive:
        print(f' - {result}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='dirb', description='Directory Buster')
    parser.add_argument('root', help='Root URL, e.g. http://example.com')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    asyncio.run(main(args.root, args.verbose, sys.stdin))
