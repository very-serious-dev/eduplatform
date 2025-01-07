import DocuURL from "../../../client/DocuURL";
import { iconImgSrc, sizeToHumanReadable } from "../../../util/Formatter";

const DocumentElement = (props) => {

    const onClickFile = () => {
        window.open(`${DocuURL}/api/v1/documents/${props.identifier}`, "_blank")
    }

    return <div className="myFilesElementContainer" onClick={onClickFile}>
        <div className="myFilesElementTitleContainer">
            <img className="myFilesElementIcon" src={iconImgSrc(props.mimeType)}></img>
            <div className="myFilesElementName">{props.name}</div>
        </div>
        <div className="myFilesElementSubtitle">{sizeToHumanReadable(props.size)}</div>
    </div>
}

export default DocumentElement;