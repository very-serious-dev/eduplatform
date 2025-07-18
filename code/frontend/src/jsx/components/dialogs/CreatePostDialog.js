import TabbedActivity from "../common/TabbedActivity";
import CreateOrEditPostForm from "../posts/CreateOrEditPostForm";

const CreatePostDialog = (props) => {

    return <div className="popupOverlayBackground" onClick={props.onDismiss}>
            <div className="popup widePopup" onClick={e => { e.stopPropagation(); }}>
                <div className="card dialogBackground">
                    <TabbedActivity tabs={[
                        {
                            title: "Nueva publicación",
                            view: <CreateOrEditPostForm postType="publication"
                                classroomId={props.classId}
                                postBeingEdited={null}
                                units={props.units}
                                submitText="Publicar"
                                showDatePicker={false}
                                showDeleteButton={false}
                                showCreateQuestionnaire={false}
                                onFinished={props.onFinished}
                                onDismiss={props.onDismiss} />
                        },
                        {
                            title: "Nueva tarea",
                            view: <CreateOrEditPostForm postType="assignment"
                                classroomId={props.classId}
                                postBeingEdited={null}
                                units={props.units}
                                submitText="Crear tarea"
                                showDatePicker={true}
                                showDeleteButton={false}
                                showCreateQuestionnaire={true}
                                onFinished={props.onFinished}
                                onDismiss={props.onDismiss} />
                        }]}
                        tabContentWidthPercentage={100}
                        showTitles={true} />
                </div>
            </div>
        </div>
}

export default CreatePostDialog;