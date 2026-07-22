import asyncio


async def generate_candidate_summary(candidate):
    await asyncio.sleep(2)

    return (
        f"{candidate.name} applied for "
        f"{candidate.role_applied}. "
        f"Skills: {', '.join(candidate.skills or [])}"
    )