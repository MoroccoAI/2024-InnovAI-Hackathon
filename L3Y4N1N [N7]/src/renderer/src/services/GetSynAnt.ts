


const getSynAnt = async (word: string) => {
    try {
        const synAnt = await window.electron.ipcRenderer.invoke("get-synonyms-antonyms", word);
        return synAnt;
    } catch (error) {
        console.error("Failed to get synonyms and antonyms:", error);
        throw error;
    }
}


export default getSynAnt;