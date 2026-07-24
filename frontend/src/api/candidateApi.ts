import api from "./axios";

export async function getCandidate(id: string) {

    const response = await api.get(
        `/candidates/${id}`
    );

    return response.data;
}

export async function getCandidates(
    offset: number,
    limit: number
) {

    const response = await api.get(
        "/candidates",
        {
            params: {
                offset,
                limit
            }
        }
    );

    return response.data;
}

export async function createScore(
    id: string,
    data: {
        category: string;
        score: number;
        note: string;
    }
) {

    const response = await api.post(
        `/candidates/${id}/scores`,
        data
    );

    return response.data;

}

export async function generateSummary(
    id: string
) {

    const response = await api.post(
        `/candidates/${id}/summary`
    );

    return response.data;

}

export async function updateInternalNotes(
    id: string,
    notes: string
) {

    const response = await api.patch(
        `/candidates/${id}/notes`,
        {
            internal_notes: notes
        }
    );

    return response.data;
}