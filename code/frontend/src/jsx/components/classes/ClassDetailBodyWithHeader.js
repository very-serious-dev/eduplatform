import { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import ClassDetailBody from "./ClassDetailBody";
import EditClassDialog from "../dialogs/EditClassDialog";
import { FeedbackContext } from "../../main/GlobalContainer";
import { bannerImageSrc } from "../../../util/Formatter";

const ClassDetailBodyWithHeader = (props) => {
    const EXPANDED_HEADER_HEIGHT = 200;
    const COLLAPSED_HEADER_HEIGHT = 60;
    const [showEditClassPopup, setShowEditClassPopup] = useState(false);
    const [amountScrolled, setAmountScrolled] = useState(0);
    const [searchedText, setSearchedText] = useState("");
    const navigate = useNavigate();
    const setFeedback = useContext(FeedbackContext);

    useEffect(() => {
        const handleScroll = (e) => {
            setAmountScrolled(e.target.scrollingElement.scrollTop);
        };
        window.addEventListener('scroll', handleScroll);
        return () => {
            window.removeEventListener('scroll', handleScroll);
        };
    }, []);

    const onClassEdited = (errorMessage) => {
        if (errorMessage === undefined) {
            setFeedback({ type: "success", message: "Clase modificada con éxito" });
            props.onShouldRefresh();
        } else {
            setFeedback({ type: "error", message: errorMessage });
        }
    }

    const onClassDeleted = (errorMessage) => {
        if (errorMessage === undefined) {
            setFeedback({ type: "success", message: "Clase eliminada con éxito" });
            navigate("/");
        } else {
            setFeedback({ type: "error", message: errorMessage });
        }
    }

    const headerHeight = () => {
        return Math.min(EXPANDED_HEADER_HEIGHT, Math.max(EXPANDED_HEADER_HEIGHT - amountScrolled, COLLAPSED_HEADER_HEIGHT));
    }

    return <>
        <EditClassDialog show={showEditClassPopup}
            onDismiss={() => { setShowEditClassPopup(false); }}
            onClassEdited={onClassEdited}
            onClassDeleted={onClassDeleted}
            classId={props.classData.id} />
        <div className="classDetailHeader" style={{ height: headerHeight() }}>
            <img className="classDetailHeaderImage" src={bannerImageSrc(props.classData.theme)} /> {/* TODO work on this*/}
            <div className="classDetailHeaderTitleSearchContainer">
                <div className="classDetailHeaderTitle">{props.classData.name}</div>
                <form className="classDetailHeaderSearchForm" onSubmit={(e) => { e.preventDefault(); }}>
                    <input type="text"
                        placeholder="🔎 Buscar..."
                        value={searchedText}
                        onChange={e => { setSearchedText(e.target.value); }}
                        required />
                    <div className="underline"></div>
                </form>
            </div>
            <div className="classDetailHeaderTopIcons">
                {props.classData.should_show_edit_button === true &&
                    <div className="classDetailHeaderIcon" onClick={() => { setShowEditClassPopup(true); }}>⚙️</div>}
                <div className="classDetailHeaderIcon" onClick={() => { navigate(-1); }}>✖️</div>
            </div>
        </div>
        <div style={{ marginTop: EXPANDED_HEADER_HEIGHT }}>
            <ClassDetailBody classData={props.classData}
                searchedText={searchedText}
                onFilterPostsByUnit={(unitName => { setSearchedText(unitName); })}
                onShouldRefresh={props.onShouldRefresh} />
        </div>
    </>
}

export default ClassDetailBodyWithHeader;