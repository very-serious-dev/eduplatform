import { useNavigate } from "react-router-dom";
import GenericCard from "../common/GenericCard";

const GroupClassesSection = (props) => {
    const navigate = useNavigate();

    const onClickClass = (id) => {
        navigate(`/classes/${id}`);
    }

    return <div className="classesSectionContainer">
        <div className="classesSectionTitle">{props.group}</div>
        <div className="classesSectionTitleUnderline"></div>
        <div className="classesSectionInnerContainer">
            {props.classes.map(c => {
                return <GenericCard additionalCssClass="classClickableGenericCard"
                    cardId={c.id}
                    title={c.name}
                    footer={c.group} 
                    onClickWithId={onClickClass}
                    skirtingBoardColor={c.color} />
                    {/* TODO: replace color by theme, appropriately*/}
            })}
        </div>
    </div>
}

export default GroupClassesSection;