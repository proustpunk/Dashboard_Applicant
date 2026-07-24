import { useEffect, useState } from "react";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";


interface Score {

    id:number;
    category:string;
    score:number;
    reviewer_id:string;
    note:string | null;

}


interface Candidate {

    id:number;
    name:string;
    email:string;
    role_applied:string;
    status:string;
    skills:string[];
    summary:string | null;

    scores:Score[];

}



export default function Candidates(){


    const navigate = useNavigate();


    const [candidates,setCandidates] =
        useState<Candidate[]>([]);



    const [status,setStatus] =
        useState("");

    const [role,setRole] =
        useState("");

    const [skill,setSkill] =
        useState("");

    const [keyword,setKeyword] =
        useState("");



    const [offset,setOffset] =
        useState(0);



    const limit = 5;



    async function fetchCandidates(){


        try{


            const response = await api.get(
                "/candidates",
                {

                    params:{

                        status: status || undefined,

                        role_applied:
                            role || undefined,

                        skill:
                            skill || undefined,

                        keyword:
                            keyword || undefined,

                        offset,

                        limit

                    }

                }
            );


            setCandidates(response.data);


        }

        catch(error){

            console.log(error);

        }

    }



    useEffect(()=>{

        fetchCandidates();

    },[offset]);




    function search(){

        setOffset(0);

        fetchCandidates();

    }





    return (

        <div className="candidates-page">


            <h1>
                Candidates
            </h1>



            <div>


                <input
                    placeholder="status"
                    value={status}
                    onChange={
                        e=>setStatus(e.target.value)
                    }
                />



                <input
                    placeholder="role"
                    value={role}
                    onChange={
                        e=>setRole(e.target.value)
                    }
                />



                <input
                    placeholder="skill"
                    value={skill}
                    onChange={
                        e=>setSkill(e.target.value)
                    }
                />



                <input
                    placeholder="keyword"
                    value={keyword}
                    onChange={
                        e=>setKeyword(e.target.value)
                    }
                />



                <button onClick={search}>
                    Search
                </button>


            </div>




            {


                candidates.map(candidate=>(


                    <div

                        className="candidate-card"

                        key={candidate.id}

                        onClick={()=>{

                            navigate(
                                `/candidates/${candidate.id}`
                            )

                        }}

                    >


                        <h3>
                            {candidate.name}
                        </h3>


                        <p>
                            {candidate.email}
                        </p>


                        <p>
                            Role:
                            {" "}
                            {candidate.role_applied}
                        </p>


                        <p>
                            Status:
                            {" "}
                            {candidate.status}
                        </p>


                    </div>


                ))

            }




            <div className="pagination">


                <button

                    disabled={offset===0}

                    onClick={()=>{

                        setOffset(
                            offset-limit
                        )

                    }}

                >

                    Previous

                </button>



                <button

                    onClick={()=>{

                        setOffset(
                            offset+limit
                        )

                    }}

                >

                    Next

                </button>


            </div>



        </div>

    )


}