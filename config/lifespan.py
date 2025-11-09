from contextlib import asynccontextmanager, AsyncExitStack


def combine_lifespans(*lifespans):

    @asynccontextmanager
    async def combined_lifespan(app):
        async with AsyncExitStack() as stack:
            for l in lifespans:  # noqa: E741
                ctx = l(app)
                await stack.enter_async_context(ctx)
            yield

    return combined_lifespan
