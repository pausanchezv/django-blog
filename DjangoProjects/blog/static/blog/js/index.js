/**
 * Class Index
 */
class Index {

    /**
     * Init Method
     * @param csrfToken
     * @param ajaxUrl
     */
    static init(csrfToken, ajaxUrl) {

        // setting csrf AJAX
        jQuery.ajaxSetup({
            data: {csrfmiddlewaretoken: csrfToken }
        });

        // ajax call arguments
        let args = {
            action: 'index_pager',
            current: 2,
            quantity: 2
        };

        /**
         * Index pagination
         */
        jQuery("#view-more").click(function() {

            jQuery.get(ajaxUrl, args, function(data) {

                if (data) {

                    jQuery.each(data, function(i, obj) {

                        let $topics = "";

                        jQuery.each(obj.topics, function(e, topic) {
                            $topics += '<a href="#" class="card-link">#' + topic + '</a>';
                        });

                        let $html = '<div class="col-md-6">' +
                            '                    <div class="card mb-3">' +
                            '                      <h3 class="card-header"><a href="/blog/' + obj.id + '/detail">' + obj.title + '</a></h3>' +
                            '                      <div class="card-body">' +
                            '                        <h5 class="card-title">Author: <strong>' + obj.username + '</strong></h5>' +
                            '                        <h6 class="card-subtitle text-muted">' + obj.pub_date + '</h6>' +
                            '                      </div>' +
                            '                        <a href="/blog/' + obj.id + '/detail">' +
                            '                            <img style="width: 100%; display: block;" src="/static/' + obj.image + '" alt="Card image">' +
                            '                        </a>' +
                            '                      <div class="card-body">' +
                            '                            <p class="card-text">' + obj.body + '</p>' +
                            '                      </div>' +
                            '                      <div class="card-body">' + $topics + '</div>' +
                            '                    </div>' +
                            '                </div>';

                        $('#articles').append($html);

                    });

                    args.current += 2;

                } else {
                    alert("There are no more articles to be shown.")
                }
            });

        });


    }
}