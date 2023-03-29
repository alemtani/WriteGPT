import Button from 'react-bootstrap/Button';

export default function More({ pagination, loadNextPage }) {
    let thereAreMore = false;
    if (pagination) {
        const { next } = pagination;
        thereAreMore = next !== null;
    }

    return (
        <div className="More">
            {thereAreMore &&
                <Button variant="outline-primary" onClick={loadNextPage}>
                    More &raquo;
                </Button>
            }
        </div>
    )
}