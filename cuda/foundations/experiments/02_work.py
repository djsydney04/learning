"""Print a work-assignment model on the CPU; this does not run in parallel.

From the repository root: python3 cuda/foundations/experiments/02_work.py
"""


def assign_jobs(job_count, workers):
    if job_count < 0 or workers < 1:
        raise ValueError("Use a nonnegative job count and at least one worker")
    rounds = []
    for first in range(0, job_count, workers):
        current_round = []
        for worker in range(workers):
            job = first + worker
            if job < job_count:
                current_round.append((worker, job))
        rounds.append(current_round)
    return rounds


def main():
    jobs = 8  # Try 10: the last round will have unused workers.
    for workers in [1, 4]:
        rounds = assign_jobs(jobs, workers)
        print(f"\n{jobs} jobs, {workers} imagined workers: {len(rounds)} rounds")
        for number, assignments in enumerate(rounds, 1):
            print(f"Round {number}: {assignments} (worker, job)")
    for job_count in [0, 1, 7, 8, 9, 10]:
        for workers in [1, 4]:
            rounds = assign_jobs(job_count, workers)
            owners = [job for row in rounds for worker, job in row]
            assert sorted(owners) == list(range(job_count))
            assert all(len(row) <= workers for row in rounds)
    print("\nPASS: each job has exactly one owner.")
    print("This is a sequential CPU model, not GPU execution or measured speed.")


if __name__ == "__main__":
    main()
