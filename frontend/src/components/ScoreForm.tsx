import { useState } from "react";


interface ScoreFormProps {

    onSubmit:(data:{
        category:string;
        score:number;
        note:string;
    })=>void;

}




export default function ScoreForm({

    onSubmit

}:ScoreFormProps){



    const [category,setCategory] =
        useState("");

    const [score,setScore] =
        useState(1);

    const [note,setNote] =
        useState("");





    function handleSubmit(
        e:React.FormEvent
    ){

        e.preventDefault();



        onSubmit({

            category,

            score,

            note

        });



        setCategory("");

        setScore(1);

        setNote("");

    }






    return (


        <form onSubmit={handleSubmit}>


            <h2>
                Add Score
            </h2>



            <input

                placeholder="Category"

                value={category}

                onChange={
                    e=>setCategory(
                        e.target.value
                    )
                }

                required

            />



            <select

                value={score}

                onChange={
                    e=>setScore(
                        Number(e.target.value)
                    )
                }

            >

                <option value={1}>
                    1
                </option>

                <option value={2}>
                    2
                </option>

                <option value={3}>
                    3
                </option>

                <option value={4}>
                    4
                </option>

                <option value={5}>
                    5
                </option>


            </select>




            <textarea

                placeholder="Note"

                value={note}

                onChange={
                    e=>setNote(
                        e.target.value
                    )
                }

            />




            <button type="submit">

                Submit Score

            </button>



        </form>


    )


}