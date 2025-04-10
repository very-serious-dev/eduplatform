import { useContext, useState } from "react";
import EduAPIFetch from "../../../client/EduAPIFetch";
import AssignmentUserStatus from "./AssignmentUserStatus";
import { FeedbackContext } from "../../main/GlobalContainer";
import AreYouSureDialog from "../dialogs/AreYouSureDialog";

const AssignmentTeacherLeftPaneContent = (props) => {
    const [isLoadingPublishAll, setLoadingPublishAll] = useState(false);
    const [showAreYouSure, setShowAreYouSure] = useState(false);
    const setFeedback = useContext(FeedbackContext);

    const numberAssigneesWhoDidntSubmit = () => {
        return props.assignmentData.assignees.reduce((acc, assignee) => {
            if (props.assignmentData.submits.some(s => s.author.username === assignee.username)) {
                return acc;
            }
            return acc + 1;
        }, 0);
    }

    const numberUnscoredSubmits = () => {
        return props.assignmentData.submits.reduce((acc, submit) => {
            if (submit.score) {
                return acc;
            }
            return acc + 1;
        }, 0);
    }

    const numberUnpublishedScores = () => {
        return props.assignmentData.submits.reduce((acc, submit) => {
            if (submit.score && submit.is_score_published === false) {
                return acc + 1;
            }
            return acc;
        }, 0);
    }

    const nAssigneesWhoDidntSubmit = numberAssigneesWhoDidntSubmit();
    const nUnscoredSubmits = numberUnscoredSubmits();
    const nUnpublishedScores = numberUnpublishedScores();

    const publishAll = () => {
        setLoadingPublishAll(true);
        EduAPIFetch("POST", `/api/v1/assignments/${props.assignmentData.id}/scores`)
            .then(json => {
                setLoadingPublishAll(false);
                if (json.success === true) {
                    setFeedback({ type: "success", message: "Calificaciones publicadas" });
                    props.onShouldRefresh();
                } else {
                    setFeedback({ type: "error", message: "Se ha producido un error" });
                }
                setShowAreYouSure(false);
            })
            .catch(error => {
                setLoadingPublishAll(false);
                setFeedback({ type: "error", message: error.error ?? "Se ha producido un error" });
                setShowAreYouSure(false);
            })
    }

    return <>
        {showAreYouSure &&
            <AreYouSureDialog onActionConfirmed={publishAll}
                onDismiss={() => { setShowAreYouSure(false); }}
                isLoading={isLoadingPublishAll}
                dialogMode="SUBMIT"
                warningMessage="¿Deseas entregar todas las calificaciones guardadas que aún no has publicado? Cada estudiante podrá ver su puntuación" />}
        <div className="assignmentDetailLeftPaneInfoContainer">
            {nAssigneesWhoDidntSubmit > 0 && <div className="assignmentDetailLeftPaneInfo">
                ℹ️ No entregada por {nAssigneesWhoDidntSubmit} {nAssigneesWhoDidntSubmit > 1 ? "estudiantes" : "estudiante"}
            </div>}
            {nUnscoredSubmits > 0 && <div className="assignmentDetailLeftPaneInfo">
                ℹ️ No has calificado {nUnscoredSubmits} {nUnscoredSubmits > 1 ? "entregas" : "entrega"}
            </div>}
            {nUnpublishedScores > 0 && <><div className="assignmentDetailLeftPaneInfo">
                ⚠️ {nUnpublishedScores} {nUnpublishedScores > 1 ? "calificaciones están" : "calificación está"} sin publicar
            </div>
                <div onClick={() => { setShowAreYouSure(true); }} className="card assignmentTeacherPanePublishAll">
                    Publicar todas
                </div>
            </>}
        </div>
        <div className="assignmentDetailLeftPaneTitle">
            💼 Trabajo de la clase
        </div>
        <div className="classDetailSectionUnderline" />
        {props.assignmentData.assignees.map(a => {
            const submit = props.assignmentData.submits.find(s => s.author.username === a.username)
            return <AssignmentUserStatus submit={submit}
                author={a}
                assignmentId={props.assignmentData.id}
                canEditScore={props.assignmentData.should_show_teacher_options /* TODO: Always true ??*/}
                onScoreChanged={props.onScoreChanged} />
        })}
    </>
}

export default AssignmentTeacherLeftPaneContent;