import asyncio
import evdev
 
dev = evdev.InputDevice('/dev/input/event2')
print(dev)

async def main(dev):
    async for ev in dev.async_read_loop():
        #print(repr(ev))
        print(evdev.categorize(ev))

if __name__ == '__main__':
    asyncio.run(main(dev))