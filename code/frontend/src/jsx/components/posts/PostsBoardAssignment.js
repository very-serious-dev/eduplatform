import { useNavigate } from "react-router-dom";
import { beautifullyDisplayDate, footNoteForDateAndAuthor } from "../../../util/Formatter";
import { ASSIGNMENT_CONTENT_NAVIGATED_FROM_WITH_ID, ASSIGNMENT_TITLE_NAVIGATED_FROM_WITH_ID } from "../../pages/AssignmentPage";

const PostsBoardAssignment = (props) => {
    const navigate = useNavigate();

    const dueDate = () => {
        if (props.post.taskDueDate === undefined) {
            return "Sin definir";
        }
        return beautifullyDisplayDate(new Date(props.post.taskDueDate));
    }

    const onClick = () => {
        sessionStorage.setItem(ASSIGNMENT_TITLE_NAVIGATED_FROM_WITH_ID(props.post.id), props.post.title);
        sessionStorage.setItem(ASSIGNMENT_CONTENT_NAVIGATED_FROM_WITH_ID(props.post.id), props.post.content);
        navigate(`/assignments/${props.post.id}`)
    }

    return <div className="card classDetailEntry classDetailEntryAssignment" onClick={onClick}>
        {props.post.unitName && <div className="classDetailEntryUnit">{props.post.unitName}</div>}
        <div className="classDetailAssignmentTitle">💼 {props.post.title}</div>
        <div className="classDetailAssignmentDueDate">Fecha de entrega: { dueDate() }</div>
        <div className="classDetailEntryFootNote">
            {footNoteForDateAndAuthor(props.post.publication_date, props.post.author)}
        </div>
    </div>
}

export default PostsBoardAssignment;