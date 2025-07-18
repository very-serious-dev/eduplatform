import { useContext, useState } from "react";
import SubmitAssignmentDialog from "../dialogs/SubmitAssignmentDialog";
import { FeedbackContext, ThemeContext } from "../../main/GlobalContainer";
import AssignmentUserStatus from "./AssignmentUserStatus";
import { accent, pointableSecondary, primary } from "../../../util/Themes";

const AssignmentStudentLeftPaneContent = (props) => {
    const [showSubmit, setShowSubmit] = useState(false);
    const setFeedback = useContext(FeedbackContext);
    const theme = useContext(ThemeContext);

    const onSubmitCreated = (errorMessage) => {
        if (errorMessage === undefined || errorMessage === "") {
            setFeedback({ type: "success", message: "Tarea entregada" });
            props.onShouldRefresh();
        } else {
            setFeedback({ type: "error", message: errorMessage });
        }
    }

    const isAssignmentPast = () => {
        const due = new Date(props.assignmentData.assignment_due_date)
        const now = new Date()
        return now > due;
    }

    return <>
        {showSubmit && <SubmitAssignmentDialog assignmentId={props.assignmentData.id}
            onDismiss={() => { setShowSubmit(false); }}
            onSubmitCreated={onSubmitCreated} />}
        <div className="assignmentDetailLeftPaneTitle">
            💼 Tu trabajo
        </div>
        <div className={`classDetailSectionUnderline ${accent(theme)}`} />
        {props.assignmentData.your_submit !== null
            ? <>
                {/* assignmentId | onScoreChanged are only needed in
                    AssignmentTeacherLeftPaneContent so as to PUT scores */ }
                <AssignmentUserStatus submit={props.assignmentData.your_submit}
                    author={props.assignmentData.your_submit.author}
                    assignmentId={null}
                    onScoreChanged={null} />
                <p>🎉 ¡Ya has entregado la tarea!</p>
            </>
            : <>
                <p>No has entregado la tarea todavía</p>
                {isAssignmentPast()
                    ? <p>😔 <i>Ya ha pasado el plazo de entrega</i></p>
                    : <div className={`card submitAssignmentButton pointable ${primary(theme)} ${pointableSecondary(theme)}`}
                        onClick={() => { setShowSubmit(true); }}>➕ Subir entrega</div>}
            </>}
    </>
}

export default AssignmentStudentLeftPaneContent;