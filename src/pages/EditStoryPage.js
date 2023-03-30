import { useState, useEffect, useRef } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { useParams, Link } from 'react-router-dom';
import Body from '../components/Body';
import InputField from '../components/InputField';
import { useApi } from '../contexts/ApiProvider';
import { useFlash } from '../contexts/FlashProvider';

export default function EditStoryPage() {
    const [formErrors, setFormErrors] = useState({});
    const { id } = useParams();
    const titleField = useRef();
    const api = useApi();
    const flash = useFlash();

    useEffect(() => {
        titleField.current.focus();
    }, [id]);

    const onSubmit = async (e) => {
        e.preventDefault();
        const title = titleField.current.value;

        const errors = {};
        if (!title) {
            errors.title = 'Prompt must not be empty.';
        }
        if (title.length > 140) {
            errors.title = 'Prompt cannot exceed 140 characters.';
        }
        setFormErrors(errors);
        if (Object.keys(errors).length > 0) {
            return;
        }

        flash('Submitted! Please wait for ChatGPT to rewrite your story.', 'info');
        const response = await api.put(`/stories/${id}`, {title});
        if (response.ok) {
            flash(
                <>
                    ChatGPT has responded to your <i>new</i> prompt: <Link to={'/story/' + response.body.id} className="story-flash">{title}</Link>
                </>, 'success'
            );
        } else {
            flash(response.body.message, 'danger');
        }
    };

    return (
        <Body sidebar={true}>
            <Form onSubmit={onSubmit}>
                <InputField
                    name="title" label="What would you like ChatGPT to write about instead?"
                    error={formErrors.title} fieldRef={titleField} />
                <Button variant="primary" type="submit">Save</Button>
            </Form>
        </Body>
    );
}