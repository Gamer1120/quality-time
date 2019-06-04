import React, { useState } from 'react';
import { Message } from 'semantic-ui-react';
import { Subjects } from '../subject/Subjects';
import { Tag } from '../widgets/Tag';
import { MetricSummaryCard } from '../dashboard/MetricSummaryCard';
import { CardDashboard } from '../dashboard/CardDashboard';
import { ReportTitle } from './ReportTitle'

function ReportDashboard(props) {
    const subject_cards = Object.entries(props.report.summary_by_subject).map(([subject_uuid, summary]) =>
        <MetricSummaryCard
            header={props.report.subjects[subject_uuid].name}
            key={subject_uuid}
            onClick={(event) => props.onClick(event, subject_uuid)}
            {...summary}
        />
    );
    const tag_cards = Object.entries(props.report.summary_by_tag).map(([tag, summary]) =>
        <MetricSummaryCard
            header={<Tag tag={tag} color={props.tags.includes(tag) ? "blue" : null} />}
            key={tag}
            onClick={() => props.setTags(tags => (tags.includes(tag) ? tags.filter((value) => value !== tag) : [tag, ...tags]))}
            {...summary}
        />
    );
    return (
        <CardDashboard big_cards={subject_cards} small_cards={tag_cards} />
    )
}

export function Report(props) {
    function navigate_to_subject(event, subject_uuid) {
        event.preventDefault();
        document.getElementById(subject_uuid).scrollIntoView();
        window.scrollBy(0, -65);  // Correct for menu bar
    }
    const [tags, setTags] = useState([]);
    if (!props.report) {
        return props.report_date ?
            <Message warning size='huge'>
                <Message.Header>{`Sorry, this report didn't exist at ${props.report_date}`}</Message.Header>
            </Message>
            :
            <Message negative size='huge'>
                <Message.Header>Sorry, this report doesn't exist</Message.Header>
            </Message>
    }
    return (
        <>
            <ReportTitle
                go_home={props.go_home}
                report={props.report}
                readOnly={props.readOnly}
                reload={props.reload}
            />
            <ReportDashboard
                onClick={(e, s) => navigate_to_subject(e, s)}
                report={props.report}
                setTags={setTags}
                tags={tags}
            />
            <Subjects
                datamodel={props.datamodel}
                nr_new_measurements={props.nr_new_measurements}
                readOnly={props.readOnly}
                reload={props.reload}
                report={props.report}
                report_date={props.report_date}
                search_string={props.search_string}
                tags={tags}
            />
        </>
    )
}