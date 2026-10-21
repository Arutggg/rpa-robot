import argparse
import asyncio


async def count(start: int) -> None:
    n = start
    while True:
        print(n, flush=True)
        n += 1
        await asyncio.sleep(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=0, help="number to start counting from")
    args = parser.parse_args()

    try:
        asyncio.run(count(args.start))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()