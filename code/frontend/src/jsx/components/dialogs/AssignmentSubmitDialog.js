import { useState } from "react";
import { beautifullyDisplayDate, beautifullyDisplayDateHour } from "../../../util/Formatter";
import PostsBoardEntryFile from "../posts/PostsBoardEntryFile";
import SetScoreDialog from "./SetScoreDialog";

const AssignmentSubmitDialog = (props) => {
    const [showSetScore, setShowSetScore] = useState(false);

    return props.show === true ? showSetScore ?
        <SetScoreDialog assignmentId={props.assignmentId}
            username={props.author.username}
            currentScore={props.submit.score}
            onSuccess={props.onScoreChanged}
            onDismiss={() => { setShowSetScore(false); }} />
        : <div className="popupOverlayBackground" onClick={props.onDismiss}>
            <div className="popup" onClick={e => { e.stopPropagation(); }}>
                <div className="card dialogBackground assignmentSubmitDialog">
                    <div className="dialogTitle">Detalles de la entrega</div>
                    <div className="assignmentSubmitDialogAuthorFullName">{`Entrega de: ${props.author.name} ${props.author.surname}`}</div>
                    <div className="assignmentSubmitDialogAuthorUsername">{`(${props.author.username})`}</div>
                    {props.submit === undefined ?
                        <div>
                            <div className="assignmentSubmitDialogDate">Fecha de entrega: ❌ No entregado </div>
                        </div>
                        :
                        <>
                            <div className="assignmentSubmitDialogDate">{`Fecha de entrega: ✔️ ${beautifullyDisplayDate(props.submit.submit_date)} (${beautifullyDisplayDateHour(props.submit.submit_date)})`}</div>
                            <div className="assignmentSubmitDialogFilesTitle">Documentos entregados:</div>
                            <div>{props.submit.files.length > 0 ?
                                <div className="assignmentSubmitDialogFiles">
                                    {props.submit.files.map(f => <PostsBoardEntryFile file={f} />)}
                                </div>
                                : <div className="assignmentSubmitDialogSectionContent">No se ha entregado ningún fichero</div>}
                            </div>
                            <div className="assignmentSubmitDialogCommentTitle">Comentario:</div>
                            <div className="assignmentSubmitDialogSectionContent">{props.submit.comment ?? "No se ha añadido ningún comentario"}</div>
                            <div className="assignmentSubmitScoreTitle">Calificación</div>
                            {props.submit.score !== undefined ?
                                <>
                                    <div className={`assignmentSubmitScore ${props.submit.is_score_published ? "scorePublished" : "scoreUnpublished"}`}>{props.submit.score}</div>
                                    {props.submit.is_score_published === false && <div className="unpublishedScoreHint">Esta puntuación no está publicada para el estudiante todavía</div>}
                                </>
                                : <div className="assignmentSubmitScoreNotReceived">🍂 No hay una calificación todavía</div>}
                            {props.canEditScore === true && <div className="card assignmentSetScoreButton" onClick={() => { setShowSetScore(true); }}>
                                ➕ Editar calificación
                            </div>}
                        </>}
                </div>
            </div>
        </div> : <></>
}

export default AssignmentSubmitDialog;