import { footNoteDateAuthor } from "../../../util/Formatter";
import FilesElementContextMenuButton from "./FilesElementContextMenuButton";

const FolderElement = (props) => {
    
    const shouldShowContextMenu = () => {
        return props.showContextMenu && props.folder.is_autogenerated !== true;
    }

    return <div className={`myFilesElementContainer myFilesElementContainerHoverable pointable ${props.selected ? "filesElementSelected" : "filesElementUnselected"}`}
        onClick={() => { props.onFolderClicked(props.folder.id, props.level) }}>
        {shouldShowContextMenu() && <FilesElementContextMenuButton folder={props.folder}
            filesTree={props.filesTree}
            onMoveDeleteSuccess={props.onMoveDeleteSuccess}
            onMoveDeleteFail={props.onMoveDeleteFail} />}
        <div className="myFilesElementTitleContainer">
            <img className="myFilesElementIcon" src="/small/icon_folder.png"></img>
            <div className="myFilesElementName">{props.folder.name}</div>
        </div>
        {props.folder.is_autogenerated && <div className="myFilesElementSpecialText">PROTEGIDO ☑️</div>}
        <div className="myFilesElementAuthorDate">{`${footNoteDateAuthor(props.folder.created_at, props.showAuthor ? props.folder.author : null)}`}</div>
    </div>
}

export default FolderElement;