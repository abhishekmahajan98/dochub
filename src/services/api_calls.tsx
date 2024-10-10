
export const fetchQueryResponse = async(queryObj:any):Promise<any> =>{
    const response = await fetch('api/v1/chat/1/12',
        {
            method: 'POST',
            body: JSON.stringify(queryObj)
        },
    );
    if(!response.ok){
        throw new Error("Fetch Failed")
    }
    const data = response.json()
    return data;
}