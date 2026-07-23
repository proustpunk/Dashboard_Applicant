interface Score {

    id: number;
    category: string;
    score: number;
    reviewer_id: string;
    note: string | null;

}

interface ScoreListProps {

    scores: Score[];

}

export default function ScoreList({

    scores

}: ScoreListProps) {

    if (scores.length === 0) {

        return (
            <p>No scores yet.</p>
        );

    }

    return (

        <div>

            <h2>Scores</h2>

            {

                scores.map(score => (

                    <div key={score.id}>

                        <p>
                            Category: {score.category}
                        </p>

                        <p>
                            Score: {score.score}/5
                        </p>

                        <p>
                            Reviewer: {score.reviewer_id}
                        </p>

                        <p>
                            Note: {score.note ?? "No note"}
                        </p>

                        <hr />

                    </div>

                ))

            }

        </div>

    );

}