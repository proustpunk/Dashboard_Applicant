import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { updateInternalNotes,getCandidate, createScore,generateSummary } from "../api/candidateApi";
import ScoreList  from "../components/scorelist";
import ScoreForm from "../components/ScoreForm";
import { getCurrentUser } from "../api/authApi";
interface User {

    email: string;
    role: string;

}

interface Score {
    id: number;
    category: string;
    score: number;
    reviewer_id: string;
    note: string | null;
}
interface Candidate {

    id: number;
    name: string;
    email: string;
    role_applied: string;
    status: string;
    skills: string[] | null;
    summary: string | null;
    internal_notes: string|null;

    scores: Score[];

}



export default function CandidateDetail(){

    const [loadingSummary, setLoadingSummary] =
    useState(false);

    const [user,setUser] =
    useState<User | null>(null);


    const { id } = useParams();


    const [candidate,setCandidate] =
        useState<Candidate | null>(null);

    const [notes, setNotes] = useState("");

    async function fetchCandidate(){

    const candidate =
        await getCandidate(id!);

    setCandidate(candidate);

    setNotes(
        candidate.internal_notes ?? ""
    );

}

    async function handleScoreSubmit(data: {
    category: string;
    score: number;
    note: string;
}) {

    if (!id) return;

    try {

        await createScore(id, data);

        await fetchCandidate();

    }

    catch (error) {

        console.error(error);

    }

}

async function handleGenerateSummary() {

    if (!id) return;

    try {

        setLoadingSummary(true);

        await generateSummary(id);

        await fetchCandidate();

    }

    catch (error) {

        console.error(error);

    }

    finally {

        setLoadingSummary(false);

    }

}

async function handleSaveNotes(){

    if(!id) return;

    try {

        await updateInternalNotes(
            id,
            notes
        );

        await fetchCandidate();

    }

    catch(error){

        console.error(error);

    }

}



    useEffect(()=>{

    fetchCandidate();

    getCurrentUser()
        .then(setUser);

},[]);



    if(!candidate){

        return <h2>Loading...</h2>

    }



    return (

        <div>

            <h1>
                {candidate.name}
            </h1>


            <p>
                Email:
                {candidate.email}
            </p>


            <p>
                Role:
                {candidate.role_applied}
            </p>


            <p>
                Status:
                {candidate.status}
            </p>



            <h2>Summary</h2>

<button
    onClick={handleGenerateSummary}
    disabled={loadingSummary}
>

    {
        loadingSummary
        ?
        "Generating..."
        :
        "Generate Summary"
    }

</button>

<p>
{
    candidate.summary
    ?
    candidate.summary
    :
    "No summary generated yet."
}
</p>

            

            <ScoreList
    scores={candidate.scores}
/>

<ScoreForm
    onSubmit={handleScoreSubmit}
/>
            


            

        {
    user?.role === "admin" && (

        <div>

            <h2>
                Internal Notes
            </h2>
<textarea
    value={notes}
    onChange={(e) => setNotes(e.target.value)}
/>
<button
    onClick={handleSaveNotes}
>
    Save Notes
</button>

        </div>

    )
}
        </div>

    )

}

