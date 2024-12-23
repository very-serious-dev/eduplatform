import { footNoteForDateAndAuthor } from "../../../util/Formatter";
import PostsBoardEntryFile from "./PostsBoardEntryFile";

const PostsBoardEntry = (props) => {
    const addLineBreaks = (str) => {
        return str.split('\n').map(subStr => <>{subStr}<br/></>);
    }

    return <div className="card classDetailEntry">
        {props.post.unit_name && <div className="classDetailEntryUnit">{props.post.unit_name}</div>}
        <div className="classDetailEntryTitle">{props.post.title}</div>
        <div className="classDetailEntryContent">{addLineBreaks(props.post.content)}</div>
        <div className="classDetailEntryFiles">
            {props.post.files.map(f => <PostsBoardEntryFile file={f} />)}
        </div>
        <div className="classDetailEntryFootNote">
            {footNoteForDateAndAuthor(props.post.publication_date, props.post.author)}
        </div>
    </div>
}

export default PostsBoardEntry;