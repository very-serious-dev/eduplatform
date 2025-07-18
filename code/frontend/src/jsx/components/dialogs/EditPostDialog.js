import { useState } from "react";
import CreateOrEditPostForm from "../posts/CreateOrEditPostForm";
import { EduAPIFetch } from "../../../client/APIFetch";
import AreYouSureDialog from "./AreYouSureDialog";

const EditPostDialog = (props) => {
    const [showAreYouSure, setShowAreYouSure] = useState(false);
    const [isLoadingDelete, setLoadingDelete] = useState(false);

    const onDeletePost = () => {
        setLoadingDelete(true);
        EduAPIFetch("POST", `/api/v1/posts/${props.post.id}/amendments`, { post_type: "amend_delete" })
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

    return showAreYouSure ?
        <AreYouSureDialog onActionConfirmed={onDeletePost}
            onDismiss={() => { setShowAreYouSure(false); }}
            isLoading={isLoadingDelete}
            dialogMode="DELETE"
            warningMessage={`¿Deseas eliminar esta publicación?`} />
        : <div className="popupOverlayBackground" onClick={e => { e.stopPropagation(); props.onDismiss() }}>
            <div className="popup widePopup" onClick={e => { e.stopPropagation(); }}>
                <div className="card dialogBackground">
                    <CreateOrEditPostForm postType="amend_edit"
                        classroomId={props.classroomId}
                        postBeingEdited={props.post}
                        units={props.units}
                        titlePlaceholder="Nuevo título"
                        contentPlaceholder="Edita aquí el contenido"
                        submitText="Publicar modificación"
                        showDatePicker={props.post.kind === "assignment"}
                        showDeleteButton={true}
                        showCreateQuestionnaire={props.post.kind === "assignment"}
                        onDeleteClicked={() => { setShowAreYouSure(true); }}
                        onFinished={props.onFinished}
                        onDismiss={props.onDismiss} />
                </div>
            </div>
        </div>
}

export default EditPostDialog;