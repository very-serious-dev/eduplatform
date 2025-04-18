import { useState } from "react";
import CreateOrEditPostForm from "../posts/CreateOrEditPostForm";
import EduAPIFetch from "../../../client/EduAPIFetch";
import AreYouSureDialog from "./AreYouSureDialog";

const EditPostDialog = (props) => {
    const [showAreYouSurePopup, setShowAreYouSurePopup] = useState(false);
    const [isLoadingDelete, setLoadingDelete] = useState(false);

    const onDeletePost = () => {
        setLoadingDelete(true);
        let body = {
            post_type: "amend_delete"
        }
        EduAPIFetch("POST", `/api/v1/posts/${props.post.id}/amendments`, body)
            .then(json => {
                setLoadingDelete(false);
                if (json.success === true) {
                    props.onFinished();
                } else {
                    props.onFinished("Se ha producido un error");
                }
                props.onDismiss();
            })
            .catch(error => {
                setLoadingDelete(false);
                props.onFinished(error.error ?? "Se ha producido un error");
                props.onDismiss();
            })
    }

    return props.show === true ? showAreYouSurePopup ?
        <AreYouSureDialog onActionConfirmed={onDeletePost}
            onDismiss={() => { setShowAreYouSurePopup(false); }}
            isLoading={isLoadingDelete}
            dialogMode="DELETE"
            warningMessage={`¿Deseas eliminar esta publicación?`} />
        : <div className="popupOverlayBackground" onClick={e => { e.stopPropagation(); props.onDismiss() }}>
            <div className="popup widePopup" onClick={e => { e.stopPropagation(); }}>
                <div className="card dialogBackground">
                    <CreateOrEditPostForm postType="amend_edit"
                        classIdForPostCreation={null}
                        postBeingEdited={props.post}
                        units={props.units}
                        titlePlaceholder="Nuevo título"
                        contentPlaceholder="Edita aquí el contenido"
                        submitText="Publicar modificación"
                        showDatePicker={props.post.kind === "assignment"}
                        showDeleteButton={true}
                        onDeleteClicked={() => { setShowAreYouSurePopup(true); }}
                        onFinished={props.onFinished}
                        onDismiss={props.onDismiss} />
                </div>
            </div></div> : <></>
}

export default EditPostDialog;