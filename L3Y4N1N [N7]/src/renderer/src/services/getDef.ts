import { ipcRenderer } from "electron";




const getDef = async (def: string) => {
    let definition = await window.electron.ipcRenderer.invoke("get-definition", def);
    return definition.definit;
};


export default getDef;