import { useState } from "react";
import LoadingHUD from "../common/LoadingHUD";
import EduAPIFetch from "../../../client/EduAPIFetch";
import DocuAPIFetch from "../../../client/DocuAPIFetch";
import DropFilesArea from "../common/DropFilesArea";

const UploadDocumentsDialog = (props) => {
    const [attachedFilesReady, setAttachedFilesReady] = useState([]);
    const [isLoading, setLoading] = useState(false);

    const onSubmitUploadFiles = (event) => {
        event.preventDefault();
        setLoading(true);
        DocuAPIFetch("POST", "/api/v1/documents", { files: attachedFilesReady })
            .then(json => {
                if (json.success === true) {
                    sendEduPostRequest(json.uploaded_files);
                } else {
                    setLoading(false);
                    setAttachedFilesReady([]);
                    props.onFail("Se ha producido un error");
                    props.onDismiss();
                }
            })
            .catch(error => {
                setLoading(false);
                setAttachedFilesReady([]);
                props.onFail(error.error ?? "Se ha producido un error");
                props.onDismiss();
            })
    }

    const sendEduPostRequest = (attachedFiles) => {
        setLoading(true);
        const body = {
            files: attachedFiles
        }
        if (props.parentFolderIdsPath.length > 0) {
            body["parent_folder_id"] = props.parentFolderIdsPath.slice(-1)[0];
        }
        EduAPIFetch("POST", "/api/v1/documents", body)
            .then(json => {
                setLoading(false);
                setAttachedFilesReady([]);
                if (json.success === true) {
                    props.onSuccess(json.result);
                } else {
                    props.onFail("Se ha producido un error");
                }
                props.onDismiss();
            })
            .catch(error => {
                setLoading(false);
                setAttachedFilesReady([]);
                props.onFail(error.error ?? "Se ha producido un error");
                props.onDismiss();
            })
    }

    return props.show === true ? <div className="popupOverlayBackground" onClick={props.onDismiss}>
        <div className="popup widePopup" onClick={e => { e.stopPropagation(); }}>
            <div className="card dialogBackground">
                <div className="dialogTitle">Subir archivos</div>
                <form onSubmit={onSubmitUploadFiles}>
                    <DropFilesArea attachedFilesReady={attachedFilesReady} setAttachedFilesReady={setAttachedFilesReady} />
                    <p>Se subirán a la siguiente carpeta:</p>
                    <div className="formInput">
                        <input className="formInputGreyBackground" type="text" value={props.parentFolderStringPath} disabled={true} />
                    </div>
                    <div className="formSubmit">
                        <input type="submit" value="Subir documentos" disabled={attachedFilesReady.length === 0}/>
                    </div>
                    {isLoading && <div className="dialogScreenHUDCentered"><LoadingHUD /></div>}
                </form>
            </div>
        </div>
    </div> : <></>
}

export default UploadDocumentsDialog;