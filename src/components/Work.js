import Stack from 'react-bootstrap/Stack';
import Image from 'react-bootstrap/Image';
import { Link } from 'react-router-dom';
import TimeAgo from './TimeAgo';

export default function Work({ work }) {
    return (
        <Stack direction="horizontal" gap={3} className="Work">
            <Image src={work.prompter._links.avatar + '&s=48'} alt={work.prompter.username} roundedCircle />
            <div>
                <p>
                    <Link to={'/work/' + work.id}>
                        {work.title}
                    </Link>
                </p>
                <p>
                    <Link to={'/prompter/' + work.prompter.id} className="prompter-link">
                        {work.prompter.username}
                    </Link>
                    &nbsp;&mdash;&nbsp;
                    <TimeAgo isoDate={work.timestamp} />
                </p>
                <p>{work.body}</p>
            </div>
        </Stack>
    )
}